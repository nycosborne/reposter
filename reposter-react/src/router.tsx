import {createBrowserRouter, Navigate, RouteObject} from "react-router-dom";
import Login from "./views/Login.tsx";
import Signup from "./views/Signup.tsx";
import DefaultLayout from "./components/DefaultLayout.tsx";
import Dashboard from "./views/Dashboard.tsx";
import GuestLayout from "./components/GuestLayout.tsx";
import PostCard from "./components/PostCard.tsx";
import AccountSettings from "./views/AccountSettings.tsx";
import ComposePost from "./views/ComposePost.tsx";
import RedirectHandler from "./apiService/RedirectHandler.tsx";
import RedditRedirectHandler from "./apiService/redditRedirectHandler.tsx";


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
            {
                path: "/account",
                element: <AccountSettings/>,
            },
            {
                path: "/compose",
                element: <ComposePost key={'new'}/>,
            },
            {
                path: "/compose/:post_id",
                element: <ComposePost key={'update'}/>,
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
        // todo: refactoter
        path: "/auth/callback/linkedin",
        element: <RedirectHandler/>,
    },
    {
        // todo: refactoter
        path: "/auth/callback/reddit",
        element: <RedditRedirectHandler/>,
    },
    {
        path: "*",
        element: <div>404 Not Found</div>,
    },
];
const router = createBrowserRouter(routerConfig);
export default router;





