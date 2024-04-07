import LandingHero from "@/components/landingHero";
import LandingNavbar from "@/components/landingNavbar";


const LandingPage = () => {
  return (
    <div className="h-full">
        <LandingNavbar />
        <LandingHero />
    </div>
  );
};

export default LandingPage;
