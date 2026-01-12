from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        # Si el usuario ya entró
        return HttpResponse(f"""
            <h1>¡Hola, {request.user.username}!</h1>
            <p>Has iniciado sesión correctamente con Keycloak.</p>
            <a href="/oidc/logout/">Cerrar Sesión</a>
        """)
    else:
        # Si el usuario no ha entrado
        return HttpResponse("""
            <h1>Bienvenido a la App de Catequesis</h1>
            <p>Por favor, identifícate para continuar.</p>
            <a href="/oidc/authenticate/">Iniciar Sesión con Keycloak</a>
        """)