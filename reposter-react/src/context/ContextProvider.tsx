import React, { createContext, useContext, ReactNode, Dispatch, SetStateAction } from 'react';

interface StateContextProps {
    user: any;
    setUser: Dispatch<SetStateAction<any>>;
    token: string | null;
    setToken: (token: string | null) => void;
}

const defaultState: StateContextProps = {
    user: null,
    setUser: () => {},
    token: null,
    setToken: () => {},
};

const StateContext = createContext<StateContextProps>(defaultState);

interface ContextProviderProps {
    children: ReactNode;
}

export const ContextProvider: React.FC<ContextProviderProps> = ({ children }) => {
    const [user, setUser] = React.useState<any>(null);
    const [token, _setToken] = React.useState<string | null>(localStorage.getItem('ACCESS_TOKEN'));

    const setToken = (token: string | null) => {
        _setToken(token);
        if (token) {
            localStorage.setItem('ACCESS_TOKEN', token);
        } else {
            localStorage.removeItem('ACCESS_TOKEN');
        }
    };

    return (
        <StateContext.Provider value={{ user, setUser, token, setToken }}>
            {children}
        </StateContext.Provider>
    );
};

export const useAppContext = () => useContext(StateContext);
