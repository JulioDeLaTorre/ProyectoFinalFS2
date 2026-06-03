from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Sala, Reserva

User = get_user_model()

class SalaModelTest(TestCase):
    def setUp(self):
        # Configuramos los datos iniciales para las pruebas
        self.sala = Sala.objects.create(
            nombre="Sala de Juntas A",
            descripcion="Una sala muy bonita",
            ubicacion="Piso 1",
            capacidad_maxima=10,
            precio_por_hora=150.00,
            precio_por_dia=1200.00,
            estado="Disponible",
            tipo_plano="oficina"
        )

    def test_sala_creacion_y_str(self):
        """Verifica que la sala se cree correctamente y su representación string sea el nombre"""
        self.assertEqual(self.sala.nombre, "Sala de Juntas A")
        self.assertEqual(str(self.sala), "Sala de Juntas A")

    def test_sala_get_absolute_url(self):
        """Verifica que la URL absoluta apunte correctamente al detalle de la sala usando su UUID"""
        url_esperada = reverse('detalle_sala', kwargs={'pk': self.sala.pk})
        self.assertEqual(self.sala.get_absolute_url(), url_esperada)

class ReservaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='password123')
        self.sala = Sala.objects.create(
            nombre="Auditorio B",
            descripcion="Auditorio grande",
            capacidad_maxima=50,
            precio_por_hora=500.00,
            precio_por_dia=4000.00
        )
        self.reserva = Reserva.objects.create(
            sala=self.sala,
            usuario=self.user,
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(hours=2),
            tipo_renta="Hora",
            costo_total=1000.00,
            estado_reserva="Pendiente"
        )

    def test_reserva_creacion(self):
        """Verifica que la reserva se asigne correctamente al usuario y a la sala"""
        self.assertEqual(self.reserva.usuario.username, 'cliente')
        self.assertEqual(self.reserva.sala.nombre, "Auditorio B")
        self.assertTrue("Reserva de cliente" in str(self.reserva))

class VistasAccesoTest(TestCase):
    def setUp(self):
        # Creamos una sala
        self.sala = Sala.objects.create(
            nombre="Sala Prueba", descripcion="Test", capacidad_maxima=5,
            precio_por_hora=50.00, precio_por_dia=400.00
        )
        
        # Creamos 3 tipos de usuarios para probar permisos
        self.user_anonimo = None # Simulado por el cliente de pruebas por defecto
        self.user_cliente = User.objects.create_user(username='mortal', password='123')
        self.user_admin = User.objects.create_superuser(username='jefe', password='123')

    def test_vistas_publicas_status_code(self):
        """Verifica que cualquier persona pueda ver el inicio, catálogo y el detalle de sala"""
        response_inicio = self.client.get(reverse('inicio'))
        self.assertEqual(response_inicio.status_code, 200)

        response_lista = self.client.get(reverse('lista_salas'))
        self.assertEqual(response_lista.status_code, 200)

        response_detalle = self.client.get(reverse('detalle_sala', kwargs={'pk': self.sala.pk}))
        self.assertEqual(response_detalle.status_code, 200)

    def test_vistas_protegidas_redirigen_login(self):
        """Verifica que un usuario sin sesión no pueda ver sus reservas (LoginRequiredMixin)"""
        response = self.client.get(reverse('lista_reservas'))
        self.assertEqual(response.status_code, 302) # Verifica que haya redirección
        
        # Obtenemos la URL dinámica de tu sistema para el login
        url_login = reverse('login')
        self.assertTrue(response.url.startswith(url_login)) # Ahora es a prueba de fallos

    def test_vistas_protegidas_acceso_permitido(self):
        """Verifica que un usuario logueado SÍ pueda entrar a sus reservas"""
        self.client.login(username='mortal', password='123')
        response = self.client.get(reverse('lista_reservas'))
        self.assertEqual(response.status_code, 200)

    def test_vista_admin_bloqueada_a_clientes(self):
        """Verifica que un cliente mortal no pueda entrar a crear salas (Error 403 Forbidden)"""
        self.client.login(username='mortal', password='123')
        response = self.client.get(reverse('sala_crear_admin'))
        self.assertEqual(response.status_code, 403)

    def test_vista_admin_permitida_a_staff(self):
        """Verifica que un administrador SÍ pueda entrar a la vista de crear salas"""
        self.client.login(username='jefe', password='123')
        response = self.client.get(reverse('sala_crear_admin'))
        self.assertEqual(response.status_code, 200)
        
class ReservaFlujoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cliente_test',
            password='password123'
        )

        self.sala = Sala.objects.create(
            nombre="Sala Flujo",
            descripcion="Sala para prueba de flujo",
            ubicacion="Piso 2",
            capacidad_maxima=10,
            precio_por_hora=100.00,
            precio_por_dia=800.00,
            estado="Disponible",
            tipo_plano="oficina"
        )

    def test_creacion_reserva_por_cliente(self):
        """Verifica que un cliente logueado pueda crear una reserva mediante POST"""

        self.client.login(username='cliente_test', password='password123')

        fecha_inicio = timezone.now() + timedelta(days=1)
        fecha_fin = fecha_inicio + timedelta(hours=2)

        datos_formulario = {
            'sala': self.sala.pk,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%dT%H:%M'),
            'tipo_renta': 'Hora',
        }

        response = self.client.post(
            reverse('reserva_crear'),
            data=datos_formulario
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reserva.objects.count(), 1)

        reserva = Reserva.objects.first()
        self.assertEqual(reserva.sala, self.sala)
        self.assertEqual(reserva.usuario, self.user)