import React from 'react';
import 'antd/dist/antd.css';

import { RegisterForm } from "./Components/RegisterForm";
import {FormData} from "./FormData";
import showSuccessNotification from "./Components/SuccessNotification";

interface OnFormFilledCallback {
    (form: FormData): any;
}

type Props = {
    onFormFilled: OnFormFilledCallback
    isSuccess: boolean
}

const RegisterPageView = (props: Props) => {

    return (<div style={{marginTop: "3%"}}>
        <RegisterForm onFormFilled={props.onFormFilled} idPrefix={"id-reg"} />
    </div>);
}

export default RegisterPageView;
