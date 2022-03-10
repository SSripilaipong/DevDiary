interface IRegistrationService {
    registerUser(username: string, password: string, displayName: string, email: string): void;
}
