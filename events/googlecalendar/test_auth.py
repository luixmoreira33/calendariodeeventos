import datetime
from actions import get_calendar_service


def test_google_calendar_auth():
    try:
        # Tenta obter o serviço - isso vai iniciar o fluxo de autenticação se necessário
        calendar_service = get_calendar_service()
        
        # Tenta listar os próximos eventos para confirmar que está funcionando
        events = calendar_service.service.events().list(
            calendarId='primary',
            maxResults=1,
            timeMin=datetime.datetime.utcnow().isoformat() + 'Z'
        ).execute()
        
        print("Autenticação bem sucedida!")
        print("Token salvo em token.json")
        print("\nPróximos eventos:")
        for event in events.get('items', []):
            print(f"- {event.get('summary')}")
            
    except Exception as e:
        print(f"Erro durante a autenticação: {str(e)}")


if __name__ == "__main__":
    test_google_calendar_auth() 
