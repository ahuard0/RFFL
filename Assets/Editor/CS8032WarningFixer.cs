using System.Linq;
using System.Xml.Linq;
using UnityEditor;

/*
 *   Removes CS8032 Warnings due to Unity 2022 bug.
 *   
 *   To use, place this file in the Assets/Editor folder, delete the .sln solution file, 
 *   close Unity and Visual Studio, then repoen Unity. The warnings should no longer appear.
 *   
 *   The Unity.SourceGenerators DLL is no longer used by newer versions of Unity.  However,
 *   newer versions of Unity still reference it, producing the Warnings.  These warnings have
 *   no impact on the ability to build a project since the DLL is not actually used.
 *   
 *   See: https://forum.unity.com/threads/vs-22-throws-cs8032-after-updating-to-tech-stream-2022-2-0f1.1372701/
 */
public class CS8032WarningFixer : AssetPostprocessor
{
    private static string OnGeneratedCSProject(string path, string content)
    {
        var document = XDocument.Parse(content);
        document.Root.Descendants()
            .Where(x => x.Name.LocalName == "Analyzer")
            .Where(x => x.Attribute("Include").Value.Contains("Unity.SourceGenerators"))
            .Remove();
        return document.Declaration + System.Environment.NewLine + document.Root;
    }
}
