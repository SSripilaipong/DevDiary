import React from 'react';
import 'antd/dist/antd.css';

import { RegisterForm } from "./Components/RegisterForm";

const RegisterPageView = () => {
    return (<div style={{marginTop: "3%"}}>
        <RegisterForm idPrefix={"id-reg"} />
    </div>);
}

export default RegisterPageView;
