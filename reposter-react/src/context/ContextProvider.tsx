import React, {createContext, useContext} from 'react';


const StateContext = createContext({
    user: null,
    setUser: () => {
    },
    token: null,
    setToken: () => {
    },
    // postId: null,
    // setPostId: () => {},
});


export const ContextProvider = ({children}: { children: React.ReactNode }) => {

    const [user, setUser] = React.useState(null)
    const [token, _setToken] = React.useState('ACCESS_TOKEN')
    // const [token, _setToken] = React.useState(localStorage.getItem('ACCESS_TOKEN'))

    const setToken = (token: string) => {
        _setToken(token)
        if (token) {
            localStorage.setItem('ACCESS_TOKEN', token)
        } else {
            localStorage.removeItem('ACCESS_TOKEN')
        }
    }
// console.log("token", token)
return (
        <StateContext.Provider value={{
            user,
            setUser,
            token,
            setToken,
        }}>
            {children}
        </StateContext.Provider>
    )
}

export const useAppContext = () => useContext(StateContext);