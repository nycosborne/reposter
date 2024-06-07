import React from 'react';
import { Outlet } from "react-router-dom";

const GuestLayout = (): React.JSX.Element => {
    return (
        <div>
            <h1>GuestLayOut</h1>
            <Outlet/>
        </div>
    )
}

export default GuestLayout; // Path: reposter-react/src/components/GuestLayout.tsx