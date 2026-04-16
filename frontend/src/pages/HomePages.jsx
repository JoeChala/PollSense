import { useNavigate } from "react-router-dom";
import "../css/HomePage.css";
import NavBar from "../components/HomePage/Navbar"

function HomePage() {
  const navigate = useNavigate();

  return (
    <>
      <NavBar />
    </>
  )
}

export default HomePage;
