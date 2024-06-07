// UseAppContext.tsx
import {useContext} from "react";
import StateContext from "./StateContext";

const useAppContext = () => useContext(StateContext);

export default useAppContext;