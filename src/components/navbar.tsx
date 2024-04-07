import { Button } from "@/components/ui/button";
import { UserButton } from "@clerk/nextjs";
import MobileSidebar from "./mobileSidebar";

const Navbar = () => {
  return (
    <div className="flex items-center p-2">
        <MobileSidebar />
        <div className="flex w-full justify-end">
            <UserButton afterSignOutUrl="/"/>
        </div>
    </div>
  )
}

export default Navbar
