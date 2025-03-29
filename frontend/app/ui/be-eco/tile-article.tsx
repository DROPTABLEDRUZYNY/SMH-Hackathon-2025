import Image from "next/image";
import Link from "next/link";

interface TileData {
    title: string;
    img_url: string;
    site_url: string;
  }
  
  export default function TileText({ tileData }: { tileData: TileData }) {
    return (
      <Link href={tileData.site_url} className="">
        <div className="w-[292px] h-[292px] flex justify-center items-center">
        <Image 
            src={tileData.img_url}
            alt={`Zdjęcie przedstawiające ${tileData.title}`}
            width={292}
            height={292}
            className="rounded-2xl"
        />
        </div>
        <label className="block text-xl text-center mt-2 capitalize">{tileData.title}</label>
      </Link>
    );
  }
  