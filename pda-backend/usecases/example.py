from usecases.usecase import UseCase

class ExampleUseCase(UseCase):
    def get_triggerwords(self) -> list[str]:
        return ["example"]

    def trigger(sefl) -> str:
        # hier kommt das periodische checken für proaktive Dinge rein.
        
        # hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

        # hier kommt der text der an den user gelesen wird hin
        return "Periodic trigger of the example usecase"

    def asked(sefl, input: str) -> str:
        return "You said: " + input
