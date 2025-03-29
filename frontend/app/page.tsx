"use client";

import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useState } from "react";
import Modal from "@/components/ui/modal";
import { PostCreationForm } from "./postCreationForm";
const FullScreenMap = dynamic(() => import("../components/ui/map"), {
  ssr: false,
});

export default function Page() {
  const [formOpened, setFormOpened] = useState(false);

  const openPostPage = (localizationID: number) => {
    setFormOpened(true);
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 bg-black mt-20">
      <main className="flex flex-col row-start-2 items-center w-full">
        <h1 className="text-6xl relative z-10 font-bold mb-8 tracking-wider text-white">
          GARBAGE COLLECTOR
        </h1>
        <p className="text-xl relative z-10 text-center max-w-2xl mb-10 text-gray-300">
          Spotted trash? Mark it on the map! Ready to clean? Access all marked
          spots and become a waste warrior. Join our mission to make Earth
          cleaner, one piece of garbage at a time.
        </p>

        {!formOpened && (
          <div className="w-full h-[50vh] bg-transparent mt-8 relative z-[50] rounded-lg">
            <FullScreenMap openPostPage={openPostPage} addingPoints={false} />
          </div>
        )}

        <div className="flex justify-center mt-[-100px] relative z-[100] bg-transparent gap-4">
          <Link href="/mark-trash">
            <button className="border-1 bg-black/40 border-white hover:bg-red-500/50 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-300">
              Mark trash
            </button>
          </Link>
          <Link href="/collect-trash">
            <button className=" bg-black/40 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-300">
              Collect trash
            </button>
          </Link>
        </div>

        {formOpened && (
          <Modal isOpen={formOpened} onClose={() => setFormOpened(false)}>
            <PostCreationForm trash_place_id={1} />
          </Modal>
        )}
      </main>
    </div>
  );
}
