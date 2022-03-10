import DummyRegistrationService from "../../Service/Registration/Dummy";
import React from "react";
import {RegisterPageController} from "./Controller";

export { RegisterPageController as RegisterPage } from "./Controller";

export const DefaultRegisterPage = () => {
    console.log("default: " + DummyRegistrationService);
    return <RegisterPageController
        redirectUrlPath={"/"}
        registrationService={new DummyRegistrationService()}
    />;
}
