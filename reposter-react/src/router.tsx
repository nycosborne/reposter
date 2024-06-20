import {createBrowserRouter, Navigate, RouteObject} from "react-router-dom";
import Login from "./views/Login.tsx";
import Signup from "./views/Signup.tsx";
import DefaultLayout from "./components/DefaultLayout.tsx";
import Dashboard from "./views/Dashboard.tsx";
import GuestLayout from "./components/GuestLayout.tsx";
import PostCard from "./components/PostCard.tsx";


const routerConfig: RouteObject[] = [
    {
        path: "/",
        element: <DefaultLayout/>,
        children: [
            {
                path: "/",
                element: <Navigate to="/dashboard"/>,
            },
            {
                path: "/posts",
                element: <PostCard/>,
            },
            {
                path: "/dashboard",
                element: <Dashboard/>,
            },
        ],
    },
    {
        path: "/",
        element: <GuestLayout/>,
        children: [
            {
                path: "/signup",
                element: <Signup/>,
            },
            {
                path: "/login",
                element: <Login/>,
            },
        ],
    },
    {
        path: "*",
        element: <div>404 Not Found</div>,
    },
];
const router = createBrowserRouter(routerConfig);
export default router;





