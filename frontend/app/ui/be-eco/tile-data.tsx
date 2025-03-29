interface TileData {
  title: string;
  text: string;
  variant?: 1 | 2 | 3;
}

export default function TileData({ tileData }: { tileData: TileData }) {
  const gradientClasses = {
    1: "bg-gradient-to-b from-red-400/30 via-transparent to-red-400/30",
    2: "bg-gradient-to-b from-yellow-400/30 via-transparent to-yellow-400/30",
    3: "bg-gradient-to-b from-green-400/30 via-transparent to-green-400/30",
  };
  const variant_classes = tileData.variant ? gradientClasses[tileData.variant] : "";

  return (
    <div className={`flex flex-col border w-full rounded-2xl  `}>
      <div className={`flex flex-row items-center justify-between rounded-2xl px-7 py-4 w-full text-3xl `}>
        <div className="min-w-0 mr-2">
          <p className="truncate font-semibold">{tileData.title}</p>
        </div>
      </div>

      <hr />

      <div className={`flex flex-col w-full px-7 py-4 text-2xl rounded-b-2xl  ${variant_classes}`}>
        <p className="pl-1 pt-2">{tileData.text}</p>
      </div>
    </div>
  );
}
