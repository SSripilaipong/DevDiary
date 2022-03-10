import {Button, Form} from "antd";
import React from "react";
import { Card } from 'antd';

import UsernameFormItem from "./UsernameFormItem";
import PasswordFormItem from "./PasswordFormItem";
import PasswordConfirmFormItem from "./PasswordConfirmFormItem";
import DisplayNameFormItem from "./DisplayNameFormItem";
import EmailFormItem from "./EmailFormItem";
import AgreementFormItem from "./AgreementFormItem";

const formItemLayout = {
    labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
    },
    wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
    },
};

const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};

type Props = {
    idPrefix: string
}

type FormData = {
    agreement: boolean
    confirm: string
    displayName: string
    email: string
    password: string
    username: string
}

export const RegisterForm = (props: Props) => {
    const { idPrefix } = props;

    const [form] = Form.useForm();

    const onFinish = (values: FormData) => {
        console.log('Received values of form: ', values);
    };

    return (<Card title={<b>ลงทะเบียน</b>} style={{ margin: "auto", width: "33%"}}>
        <Form
            {...formItemLayout}
            form={form}
            name="register"
            onFinish={onFinish}
            scrollToFirstError
        >
            <UsernameFormItem id={`${idPrefix}-username`} />
            <PasswordFormItem id={`${idPrefix}-password`} />
            <PasswordConfirmFormItem id={`${idPrefix}-passwordConfirm`} />
            <DisplayNameFormItem id={`${idPrefix}-displayName`} />
            <EmailFormItem id={`${idPrefix}-email`} />

            <AgreementFormItem id={`${idPrefix}-agree`} tailFormItemLayout={tailFormItemLayout} />
            <Form.Item {...tailFormItemLayout}>
                <Button type="primary" htmlType="submit" id={`${idPrefix}-submit"`}>
                    Register
                </Button>
            </Form.Item>
        </Form>
    </Card>);
};
