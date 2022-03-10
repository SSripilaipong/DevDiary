import React from "react";
import RegisterPageView from "./View";

type Props = {

}

type State = {

}

export class RegisterPageController extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
    }

    render() {
        return <RegisterPageView />;
    }
}
