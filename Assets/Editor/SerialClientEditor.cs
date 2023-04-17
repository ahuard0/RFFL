using UnityEngine;
using UnityEditor;

namespace Huard.Serial
{
    [CustomEditor(typeof(SerialClient))]
    public class SerialClientEditor : Editor
    {
        private string _messageToSend = "";

        /*
        *      Called when the inspector is drawn
        *      
        *      Parameters
        *      ----------
        *      None
        *      
        *      Returns
        *      -------
        *      None
        */
        public override void OnInspectorGUI()
        {
            SerialClient _SerialClient = (SerialClient)target;  // Inherited Target

            DrawDefaultInspector();

            GUILayout.Label("");

            EditorGUILayout.BeginHorizontal();
            GUILayout.Label("Send Message:");
            _messageToSend = GUILayout.TextField(_messageToSend, 200, GUILayout.Width(200));
            if (GUILayout.Button("Send", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage(_messageToSend);
            }
            EditorGUILayout.EndHorizontal();

            GUILayout.Label("");

            GUILayout.Label("Read from Device:");
            if (GUILayout.Button("Read", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.readMessage();
            }
            if (GUILayout.Button("Single Read Data", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_SINGLE_READ");
                _SerialClient.readMessage();
            }
            if (GUILayout.Button("Broadcast Data ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_BROADCAST_ON");
                _SerialClient.readBroadcast = true;
            }
            if (GUILayout.Button("Broadcast Data OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_BROADCAST_OFF");
                _SerialClient.readBroadcast = false;
            }
            if (GUILayout.Button("D0 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D0_ON");
            }
            if (GUILayout.Button("D0 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D0_OFF");
            }
            if (GUILayout.Button("D1 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D1_ON");
            }
            if (GUILayout.Button("D1 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D1_OFF");
            }
            if (GUILayout.Button("D2 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D2_ON");
            }
            if (GUILayout.Button("D2 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D2_OFF");
            }
            if (GUILayout.Button("D3 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D3_ON");
            }
            if (GUILayout.Button("D3 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D3_OFF");
            }
            if (GUILayout.Button("D4 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D4_ON");
            }
            if (GUILayout.Button("D4 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D4_OFF");
            }
            if (GUILayout.Button("D5 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D5_ON");
            }
            if (GUILayout.Button("D5 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D5_OFF");
            }
            if (GUILayout.Button("D6 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D6_ON");
            }
            if (GUILayout.Button("D6 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D6_OFF");
            }
            if (GUILayout.Button("D7 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D7_ON");
            }
            if (GUILayout.Button("D7 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D7_OFF");
            }
            if (GUILayout.Button("D8 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D8_ON");
            }
            if (GUILayout.Button("D8 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D8_OFF");
            }
            if (GUILayout.Button("D9 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D9_ON");
            }
            if (GUILayout.Button("D9 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D9_OFF");
            }
            if (GUILayout.Button("D10 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D10_ON");
            }
            if (GUILayout.Button("D10 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D10_OFF");
            }
            if (GUILayout.Button("D11 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D11_ON");
            }
            if (GUILayout.Button("D11 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D11_OFF");
            }
            if (GUILayout.Button("D12 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D12_ON");
            }
            if (GUILayout.Button("D12 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D12_OFF");
            }
            if (GUILayout.Button("D13 ON", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D13_ON");
            }
            if (GUILayout.Button("D13 OFF", GUILayout.ExpandWidth(false)))
            {
                _SerialClient.sendMessage("_D13_OFF");
            }

        }
    }
}
