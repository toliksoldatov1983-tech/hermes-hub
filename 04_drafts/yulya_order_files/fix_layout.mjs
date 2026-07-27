import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path = "./output/Юля_фасады_выборка_90_Малярка.xlsx";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path));
for (const name of ["6010-R90B", "1000-N"]) {
  wb.worksheets.getItem(name).getRange("A:A").format.columnWidth = 18;
}
const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(path);
for (const [sheetName, filename, range] of [
  ["6010-R90B", "paint6010.png", "A1:J34"],
  ["1000-N", "paint1000.png", "A1:J23"],
]) {
  const blob = await wb.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`./output/${filename}`, new Uint8Array(await blob.arrayBuffer()));
}
console.log((await wb.inspect({kind:"table",range:"Общий итог!A3:D6",include:"values,formulas",tableMaxRows:10,tableMaxCols:4})).ndjson);
