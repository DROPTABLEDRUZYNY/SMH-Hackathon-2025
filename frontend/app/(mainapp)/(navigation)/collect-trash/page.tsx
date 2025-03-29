"use client";

// import { ProfileForm } from "@/app/ui/contact/contactForm";
import FullScreenMap from "@/components/ui/map";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import Modal from "@/components/ui/modal";
import { PostCreationForm } from "@/app/postCreationForm";

export default function Page() {
    const [formOpened, setFormOpened] = useState(false)

    const openPostPage = (localizationID: number) => {
      setFormOpened(true)
    }

  return (
    <>
      <div className="top-0 left-0 w-full h-full fixed z-[10]">
        <FullScreenMap openPostPage={openPostPage} addingPoints={false} />
      </div>
      <div className="fixed bottom-10 left-0 right-0 flex justify-center items-center z-[100]"></div>
      
      {formOpened && (
              <Modal isOpen={formOpened} onClose={() => setFormOpened(false)}>
                <PostCreationForm trash_place_id={1} />
              </Modal>
        )}
    </>
  );
}
