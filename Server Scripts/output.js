// var attributeToUse = "";
// if( DocumentType == "Article" ) {
//     attributeToUse = "Customer Name";
// } else if( DocumentType == "Resume" ) {
//     attributeToUse = "Applicant's Name";
// } else if( DocumentType == "Brochure" ) {
//     attributeToUse = "Product Name";
// }
// if( attributeToUse == "" ) {
//     return;
// }
// var attributeValue = retrieveAttributeValue( attributeToUse );
// if( attributeValue == "" ) {
//     return;
// }
// var fso = new ActiveXObject("Scripting.FileSystemObject");
// for( i = 0; i < OutputFormats.Count; i++ ) {
//     var format = OutputFormats.Item( i );
//     var folderPath = format.OutputLocation;
//     folderPath = fso.BuildPath( folderPath, JobProperties.Subfolder );
//     var outputFiles = format.OutputFiles;
//     for( j = 0; j < outputFiles.Count; j++ ) {
//         var initialName = outputFiles.Item( j );
//         var slashPosition = initialName.lastIndexOf( "\\" );
//         if( slashPosition != -1 ) {
//             var subPath = initialName.substring( 0, slashPosition );
//         }
//         var initialExt = fso.GetExtensionName( initialName );
//         var sourcePath = fso.BuildPath( folderPath, initialName );
//         var sourceFolder = fso.GetParentFolderName( sourcePath );
//         var destPath = fso.BuildPath( sourceFolder, attributeValue + "." + initialExt );
//         if( fso.FileExists( destPath ) ) {
//             fso.DeleteFile( destPath );
//         }
//         fso.MoveFile( sourcePath, destPath );
//         var attributesFilePath = fso.BuildPath( sourceFolder, attributeValue + "-attr.txt" );
//         var attributesFile = fso.OpenTextFile( attributesFilePath, 2, true, -1 );
//         for( k = 0; k < Attributes.Count; k++ ) {
//             var attribute = Attributes.Item( k );
//             var attributeType = attribute.Type;
//             var attributeName = attribute.Name;
//             attributesFile.Write( attributeName + ": " );
//             if( attributeType == 0 ) { //boolean
//                 attributesFile.Write( attribute.Value ? "true" : "false" );
//             } else if( attributeType == 3 ) { //multiple lines
//                 var lines = attribute.Value;
//                 for( l = 0; l < lines.Count; l++ ) {
//                     attributesFile.Write( lines.Item( l ) + "\r\n" );
//                 }
//             } else {
//                 attributesFile.Write( attribute.Value );
//             }
//             attributesFile.Write( "\r\n" );
//         }
//         attributesFile.Close();
//     }
// }
// function retrieveAttributeValue( name )
// {
//     for( i = 0; i < Attributes.Count; i++ ) {
//         var attribute = Attributes.Item( i );
//         if( attribute.Name == name ) {
//             return attribute.Value;
//         }
//     }
// }
//
