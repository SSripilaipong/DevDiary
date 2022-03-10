export default class DummyRegistrationService implements IRegistrationService {
    private readonly registrationSuccess: boolean;

    constructor(registrationSuccess: boolean = true) {
        this.registrationSuccess = registrationSuccess;
    }
    registerUser(username: string, password: string, displayName: string, email: string): boolean {
        console.log(`DummyRegistrationService: user registered (${username}, ${password}, ${displayName}, ${email})`);
        return this.registrationSuccess;
    }
}
