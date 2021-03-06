from typing import Optional, TYPE_CHECKING

from chamber.message.bus import MessageBus
from chamber.registry import ChamberRegistry
from domain.clock import Clock, RealClock


class Registry(ChamberRegistry):
    def __init__(self):
        super().__init__()
        self.APP_NAME: str = "prod"
        self.clock: Clock = RealClock()
        self.all_registrations: Optional[AllRegistrations] = None
        self.all_users: Optional[AllUsers] = None
        self.email_service: Optional[EmailService] = None
        self.secret_manager: Optional[SecretManager] = None
        self.message_bus: Optional[MessageBus] = None


if TYPE_CHECKING:
    from domain.identity.registration.repository import AllRegistrations
    from domain.identity.user.repository import AllUsers
    from domain.identity.email.service import EmailService
    from domain.identity.security.secret import SecretManager
