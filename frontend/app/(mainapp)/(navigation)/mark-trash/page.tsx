// import { ProfileForm } from "@/app/ui/contact/contactForm";
import FullScreenMap from "@/components/ui/map";
import { Button } from "@/components/ui/button";

export default function Page() {
  return (
    <>
      <div className="top-0 left-0 w-full h-full fixed z-[10]">
        <FullScreenMap addingPoints={true} />
      </div>
      <div className="fixed bottom-10 left-0 right-0 flex justify-center items-center z-[100]"></div>
    </>
  );
}
