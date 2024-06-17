import React, {ReactNode} from 'react';
import StateContext from "./StateContext";

interface ContextProviderProps {
    children: ReactNode;
}

export const ContextProvider: React.FC<ContextProviderProps> = ({children}) => {
    const [user, _setUser] = React.useState<number | null>(null);
    // const [token, _setToken] = React.useState<string | null>('ACCESS_TOKEN');
    const [token, _setToken] = React.useState<string | null>(localStorage.getItem('ACCESS_TOKEN'));

    const setToken = (token: string | null) => {
        _setToken(token);
        if (token) {
            if (typeof token === "string") {
                localStorage.setItem('ACCESS_TOKEN', token);
            }
        } else {
            localStorage.removeItem('ACCESS_TOKEN');
        }
    };

    const setUser = (user: number | null) => {
        _setUser(user)
        // if (user.is_admin === 0) {
        //     setIsAdmin(false);
        // } else {
        //     setIsAdmin(true);
        // }
    }

    return (
        <StateContext.Provider value={{user, setUser, token, setToken}}>
            {children}
        </StateContext.Provider>
    );
};

// export const useAppContext = () => useContext(StateContext);
