"use client";

import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useState } from "react";
const FullScreenMap = dynamic(() => import("../components/ui/map"), { ssr: false });


export default function Page() {

  const openPostPage = (localizationID: number) => {
    console.info("POST PAGE OPENED")
  }
  
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 bg-black mt-20">
      <main className="flex flex-col row-start-2 items-center w-full">
        <h1 className="text-6xl font-bold mb-8 tracking-wider text-white">
          GARBAGE COLLECTOR
        </h1>
        {}
        <p className="text-xl text-center max-w-2xl mb-10 text-gray-300">
          Spotted trash? Mark it on the map! Ready to clean? Access all marked
          spots and become a waste warrior. Join our mission to make Earth
          cleaner, one piece of garbage at a time.
        </p>

        <div className="w-full h-[50vh] bg-green-900 mt-8 rounded-lg">
          <FullScreenMap openPostPage={openPostPage} addingPoints={false} /> 
        </div>

        <div className="flex justify-center mt-4 gap-4">
          <button className="border-2 border-white hover:bg-green-300/50 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-300">
            Mark trash
          </button>
          <button className="bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-300">
            Collect trash
          </button>
        </div>


        {/* <Link href={"/activity"}>
          <button
            className="shadow-[inset_0_0_0_2px_#616467] text-black px-12 py-4 rounded-full tracking-widest 
        uppercase font-bold bg-transparent hover:bg-[#616467] hover:text-white dark:text-neutral-200 
        transition duration-200"
          >
            {" "}
            Let's LiveActive!{" "}
          </button>
        </Link> */}
      </main>
    </div>
  );
}
