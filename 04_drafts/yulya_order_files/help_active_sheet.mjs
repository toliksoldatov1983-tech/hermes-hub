import { Workbook } from "@oai/artifact-tool";
const wb = Workbook.create();
console.log(wb.help("worksheet.activate", {include:"index,examples,notes",maxChars:3000}).ndjson);
console.log(wb.help("worksheets order", {search:"position|move|order|active",include:"index,examples,notes",maxChars:5000}).ndjson);
