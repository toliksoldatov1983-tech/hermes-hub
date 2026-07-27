import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

for (const path of [
  "C:/Users/user/Desktop/Юля_фасады_выборка_90_Corel.xlsx",
  "C:/Users/user/Desktop/Юля_фасады_выборка_90_Малярка.xlsx",
]) {
  const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path));
  console.log(`FILE: ${path}`);
  console.log((await wb.inspect({kind:"sheet",include:"id,name",maxChars:3000})).ndjson);
  console.log((await wb.inspect({kind:"table",maxChars:6000,tableMaxRows:8,tableMaxCols:10})).ndjson);
}
