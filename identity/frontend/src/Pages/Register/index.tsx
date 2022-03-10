import React from "react";
import {RegisterPageController} from "./Controller";

export { RegisterPageController as RegisterPage } from "./Controller";
import DummyRegistrationService from "../../Service/Registration/Dummy";

export const DefaultRegisterPage = () => {
    return <RegisterPageController
        redirectUrlPath={"/"}
        registrationService={new DummyRegistrationService()}
    />;
}
