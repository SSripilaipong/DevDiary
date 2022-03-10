import DummyRegistrationService from "../../Service/Registration/Dummy";
import React from "react";
import {RegisterPageController} from "./Controller";

export { RegisterPageController as RegisterPage } from "./Controller";

export const DefaultRegisterPage = () => {
    return <RegisterPageController
        redirectUrlPath={"/"}
        registrationService={new DummyRegistrationService()}
    />;
}
