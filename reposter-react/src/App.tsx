import {RouterProvider} from "react-router-dom";
import router from "./router";
import {ContextProvider} from "./context/ContextProvider.tsx";


function App(): JSX.Element {  // Explicitly typing the return type
    return (
        <ContextProvider>
            <RouterProvider router={router}/>
        </ContextProvider>
    );
}

export default App;
