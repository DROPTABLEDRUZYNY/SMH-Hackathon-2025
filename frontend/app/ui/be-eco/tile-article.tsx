import Image from "next/image";
import Link from "next/link";

interface TileData {
    title: string;
    img_url: string;
    site_url: string;
}
  
export default function TileText({ tileData }: { tileData: TileData }) {
    return (
      <Link href={tileData.site_url} className="group">
        <div className="w-[292px] h-[292px] flex justify-center items-center mx-auto overflow-hidden rounded-2xl bg-white/5 backdrop-blur-lg border border-white/10 hover:border-white/20 transition-all duration-300">
          <Image 
            src={tileData.img_url}
            alt={`Zdjęcie przedstawiające ${tileData.title}`}
            width={292}
            height={292}
            className="rounded-2xl object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
        <h3 className="block text-xl text-center mt-4 text-gray-200 group-hover:text-white transition-colors duration-300">{tileData.title}</h3>
      </Link>
    );
}
  