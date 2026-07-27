import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const path="C:/Users/user/Desktop/Юля_фасады_выборка_90_Малярка.xlsx";
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
console.log((await wb.inspect({kind:"sheet",include:"id,name",maxChars:3000})).ndjson);
console.log((await wb.inspect({kind:"table",range:"6010-R90B!A8:I30",include:"values,formulas",tableMaxRows:30,tableMaxCols:9,tableMaxCellChars:120})).ndjson);
for(const term of ["Обкат","торцы","одной лицевой","минимальный"]){console.log(term+": "+(await wb.inspect({kind:"match",searchTerm:term,options:{maxResults:20},summary:term})).ndjson);}
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"errors"})).ndjson);
