# Contexto
Se precisa un sistema que sirva como backend para un sistema de compra de tickets.

## Operativa
El usuario realiza el login para entrar a la plataforma, compra la entrada y realia el logout.

## Requisitos
- El sistema debe ofrecer los endopoints necesarios para cubrir la operativa:
1. Login
2. Comprar
3. Logout
4. Listar los tickets adquiridos por usuario
- El sistema debe verificar que el usuario no ha realizado el login dos veces simultaneamente
- Se debe utilizar Redis como almacenamiento
- cuando un nuevo usuario realiza el login, el sistema debe almacenarlo
- se debe utilizar dos estructuras de datos distintas, además de un índice