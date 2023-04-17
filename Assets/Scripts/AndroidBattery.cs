using UnityEngine;

namespace Huard.Utility.Android
{
    public class AndroidBattery : MonoBehaviour
    {
        void Start()
        {
            string msg = "Battery Level: " + (GetBatteryLevel() * 100) + "%";
            ShowToast(msg);
        }
        //method that calls our native plugin.
        public void ShowToast(string msg)
        {
            if (Application.platform == RuntimePlatform.Android)
            {
                // Retrieve the UnityPlayer class.
                AndroidJavaClass unityPlayerClass = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
                // Retrieve the UnityPlayerActivity object 
                AndroidJavaObject unityActivity = unityPlayerClass.GetStatic<AndroidJavaObject>("currentActivity");
                // Retrieve the "Bridge" from our native plugin.
                // ! Notice we define the complete package name.              
                AndroidJavaObject alert = new AndroidJavaObject("com.huard.serial.Alert");
                // Setup the parameters we want to send to our native plugin.              
                object[] parameters = new object[2];
                parameters[0] = unityActivity;
                parameters[1] = msg;
                // Call PrintString in bridge, with our parameters.
                alert.Call("PrintString", parameters);
            }
        }
        public float GetBatteryLevel()
        {
            if (Application.platform == RuntimePlatform.Android)
            {
                AndroidJavaClass unityPlayerClass = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
                AndroidJavaObject unityActivity = unityPlayerClass.GetStatic<AndroidJavaObject>("currentActivity");
                AndroidJavaObject batt = new AndroidJavaObject("com.huard.serial.BatteryLevelIndicator");
                object[] parameters = new object[1];
                parameters[0] = unityActivity;
                return batt.Call<float>("GetBatteryPct", parameters);
            }
            return -1f;
        }
    }
}
