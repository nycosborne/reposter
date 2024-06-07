import React from 'react';
import {Navigate, Outlet} from "react-router-dom";
import {useAppContext} from "../context/ContextProvider.tsx";

const DefaultLayout = (): React.JSX.Element => {

    const {token}: any = useAppContext();

    if (!token) {
        return <Navigate to="/login"/>
    }

    return (
        <div>
            <h1>DefaultLayout</h1>
            <Outlet/>
        </div>
    )
}

export default DefaultLayout; // Path: reposter-react/src/components/DefaultLayout.tsx