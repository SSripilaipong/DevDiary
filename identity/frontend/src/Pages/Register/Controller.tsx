import React from "react";
import RegisterPageView from "./View";
import {FormData} from "./FormData";
import showSuccessNotification from "./Components/SuccessNotification";

type Props = {
    redirectUrlPath: string
    registrationService: IRegistrationService
}

type State = {
    status: string
}

export class RegisterPageController extends React.Component<Props, State> {
    private registrationService: IRegistrationService;

    constructor(props: Props) {
        super(props);
        this.registrationService = props.registrationService;
        this.state = {status: ""};
        console.log(this.registrationService);
    }

    onFormFilled = (form: FormData) => {
        this.registrationService.registerUser(form.username, form.password, form.displayName, form.email);
        showSuccessNotification();
    }

    render() {
        const isSuccess = this.state.status == "success";
        return <RegisterPageView isSuccess={isSuccess} onFormFilled={this.onFormFilled}/>;
    }
}
