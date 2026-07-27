import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path="./output/Юля_фасады_выборка_90_Малярка.xlsx";
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem("Общий итог");

s.getRange("C19").values=[[35000]];
s.getRange("D19").formulas=[["=B19*C19"]];
s.getRange("E19").values=[["Рассчитано"]];
s.getRange("D20").formulas=[["=SUM(D17:D19)"]];
s.getRange("E20").values=[["Все типы включены"]];
s.getRange("D21").formulas=[["=SUM(D17:D19)"]];
s.getRange("E21").values=[["Рассчитано"]];
s.getRange("A21:E21").format={fill:"#C6E0B4",font:{bold:true,color:"#006100"},borders:{preset:"all",style:"medium",color:"#70AD47"}};
s.getRange("C17:D21").format.numberFormat='#,##0.00 "₸"';
s.getRange("A32").values=[["Полная стоимость включает витрины по ставке 35 000 ₸/м²."]];

const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path);
const preview=await wb.render({sheetName:"Общий итог",range:"A1:E32",scale:1.2,format:"png"});await fs.writeFile("./output/full_pricing_summary.png",new Uint8Array(await preview.arrayBuffer()));
console.log((await wb.inspect({kind:"table",range:"Общий итог!A3:E32",include:"values,formulas",tableMaxRows:35,tableMaxCols:5,tableMaxCellChars:130})).ndjson);
console.log((await wb.inspect({kind:"table",range:"6010-R90B!A3:I33",include:"values,formulas",tableMaxRows:40,tableMaxCols:9,tableMaxCellChars:100})).ndjson);
console.log((await wb.inspect({kind:"table",range:"1000-N!A3:I22",include:"values,formulas",tableMaxRows:30,tableMaxCols:9,tableMaxCellChars:100})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"})).ndjson);
