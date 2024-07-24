import {RouterProvider} from "react-router-dom";
import {ContextProvider} from "./context/ContextProvider.tsx";
import router from "./router";

function App(): JSX.Element {  // Explicitly typing the return type
    return (
        <ContextProvider>
            <RouterProvider router={router}/>
        </ContextProvider>
    );
}

export default App;
