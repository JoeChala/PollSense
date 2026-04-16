import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePages"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Home Page */}
        <Route path="/" element={<HomePage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
