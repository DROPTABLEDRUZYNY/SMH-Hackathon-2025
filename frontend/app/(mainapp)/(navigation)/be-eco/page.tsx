import TileText from "@/app/ui/be-eco/tile-article";
import TilesData from "@/app/ui/be-eco/tiles-data";

export default function Page() {
  const tilesDataFood = [
    {
      title: "Ciasto marchewkowe fit",
      img_url: "/zdrowie/articles/ciasto-marchewkowe-fit.png",
      site_url:
        "https://zycieseniora.com/kulinaria/ciasto-marchewkowe-w-wersji-fit-prosty-przepis",
    },
    {
      title: "Krem grzybowy",
      img_url: "/zdrowie/articles/krem-grzybowy.png",
      site_url:
        "https://zycieseniora.com/kulinaria/krem-grzybowy-z-siekana-rukola-i-parmezanem",
    },
    {
      title: "papryka fit",
      img_url: "/zdrowie/articles/papryka-fit.png",
      site_url:
        "https://zycieseniora.com/kulinaria/papryka-faszerowana-fit-przepis-na-czasie",
    },
    {
      title: "potrawka z podgrzybkow",
      img_url: "/zdrowie/articles/potrawka-z-podgrzybkow.png",
      site_url: "https://zycieseniora.com/kulinaria/potrawka-z-podgrzybkow  ",
    },
    {
      title: "salatka z burakami",
      img_url: "/zdrowie/articles/salatka-z-burakami.png",
      site_url:
        "https://zycieseniora.com/kulinaria/salatka-z-pieczonymi-burakami-gruszka-i-kozim-serem",
    },
    {
      title: "salatka z serem feta",
      img_url: "/zdrowie/articles/salatka-z-serem-feta.png",
      site_url:
        "https://zycieseniora.com/kulinaria/salatka-z-pieczonych-burakow-z-feta",
    },
    {
      title: "Salmorejo",
      img_url: "/zdrowie/articles/Salmorejo.png",
      site_url:
        "https://zycieseniora.com/kulinaria/salmorejo-przepis-na-hiszpanski-chlodnik-pomidorowy",
    },
    {
      title: "smoothie",
      img_url: "/zdrowie/articles/smoothie.png",
      site_url:
        "https://zycieseniora.com/kulinaria/zielone-smoothie-przepis-koktajl",
    },
  ];

const tilesDataEco = [
    { title: "artykul", img_url: "/be-eco/articles-eco/eco1.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco2.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco3.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco4.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco5.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco6.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco7.jpg", site_url: "/" },
    { title: "artykul", img_url: "/be-eco/articles-eco/eco8.jpg", site_url: "/" },
];

  return (
    <div className="flex flex-col md:flex-col gap-4 md:overflow-hidden mt-20">
      <TilesData />
      <hr></hr>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 px-2">
        {/* {tilesDataFood.map((data, index) => (
          <TileText key={index} tileData={data} />
        ))} */}
        {tilesDataEco.map((data, index) => (
          <TileText key={index} tileData={data} />
        ))}
      </div>
    </div>
  );
}
