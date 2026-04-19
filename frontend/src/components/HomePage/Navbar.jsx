import { useNavigate } from "react-router-dom";
import logo from "../../assets/pollsense_dark.png";

function NavBar() {
  return (
    <div className="flex items-center justify-between px-16 py-4 bg-[#0b0f1a]">
      {/* Left */}
      <div className="flex items-center">
        <div className="w-6 h-6 overflow-hidden">
          <img
            src={logo}
            className="w-full h-full object-contain scale-[0.4]"
          />
        </div>
        <h2 className="text-white font-semibold text-lg">PollSense</h2>
      </div>

      {/* Center */}
      <div className="flex">
        <h4 className="text-white cursor-pointer mr-4">Features</h4>
        <h4 className="text-white cursor-pointer mr-4">Take Survey</h4>
        <h4 className="text-white cursor-pointer">About</h4>
      </div>
      {/*}
      <div>
        <h4 style={{display:"inline-block",marginRight:"20px"}}>One</h4>
        <h4 style={{display:"inline-block",marginRight:"20px"}}>Twi</h4>
        <h4 style={{display:"inline-block"}}>Three</h4>
      </div>*/}

      {/* Right */}
      <div className="flex items-center gap-3">
        <button className="text-white border border-gray-600 px-4 py-1.5 rounded-md text-sm hover:border-white">
          Login
        </button>
        <button className="bg-white text-black px-4 py-1.5 rounded-md text-sm font-medium">
          Sign Up
        </button>
      </div>
    </div>
  );
}

export default NavBar;
