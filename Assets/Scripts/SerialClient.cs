using System;
using System.IO;
using System.IO.Ports;
using TMPro;
using UnityEngine;
using UnityEngine.Android;

namespace Huard.Serial
{
    public class SerialClient : MonoBehaviour
    {
        private const string _headerSend = "$";
        private string _messageRecieved;
        private string _messageSend;
        static SerialPort _serialPort;
        public bool readBroadcast = false;

        public TextMeshPro status;

        void Start()
        {
            GameObject PortsMessage = GameObject.Find("PortsMessage");
            TextMeshPro TextPorts = PortsMessage.GetComponent<TextMeshPro>();

            GameObject PortsAvailableMessage = GameObject.Find("PortsAvailableMessage");
            TextMeshPro TextPortsAvailable = PortsAvailableMessage.GetComponent<TextMeshPro>();

            TextPorts.text = "Starting...";
            TextPortsAvailable.text = "Scanning for ports...";

            // Get Ports
            string port;
            if (Application.platform == RuntimePlatform.WindowsPlayer)
                port = "COM10";
            else if (Application.platform == RuntimePlatform.WindowsEditor)
                port = "COM10";
            else if (Application.platform == RuntimePlatform.Android)
                port = "/dev/bus/usb/001/002";
            else
                port = "Platform not found";

            TextPorts.text = port;

            try
            {
                _serialPort = new SerialPort(port, 9600, Parity.None, dataBits: 8, StopBits.One);
                _serialPort.ReadTimeout = 200;
                _serialPort.WriteTimeout = 200;
            }
            catch (Exception e)
            {
                TextPortsAvailable.text = e.Message;
            }
            
            
            sendMessage("_BROADCAST_ON");
            readBroadcast = true;
        }

        void Update()
        {
            if (readBroadcast)
                readMessage();
        }

        public void updateStatus(string msg)
        {
            status.text = msg;
        }

        public void sendMessage(string msg)
        {

            if (_serialPort == null)
            {
                Debug.Log("Not Initialized");
                return;
            }

            try
            {
                if (!_serialPort.IsOpen)
                    _serialPort.Open();

                _messageSend = _headerSend + "|" + msg;
                _serialPort.WriteLine(_messageSend);
                Debug.Log("Wrote: " + _messageSend);
                _serialPort.Close();
            }
            catch (TimeoutException)
            {
                Debug.Log("Timeout");
                _serialPort.Close();
            }
            catch (IOException)
            {
                Debug.Log("I/O Blocked");
                _serialPort.Close();
            }
        }

        public string readMessage()
        {
            if (_serialPort == null)
            {
                updateStatus("Not Initialized");
                Debug.Log("Not Initialized");
                return null;
            }

            try
            {
                if (!_serialPort.IsOpen)
                    _serialPort.Open();

                _messageRecieved = _serialPort.ReadLine();
                Debug.Log(_messageRecieved);
                _serialPort.Close();
                updateStatus(_messageRecieved);
                return _messageRecieved;
            }
            catch (TimeoutException)
            {
                updateStatus("Timeout");
                Debug.Log("Timeout");
                _serialPort.Close();
                return null;
            }
            catch (IOException e)
            {
                updateStatus(e.Message);
                Debug.Log(e.Message);
                _serialPort.Close();
                return null;
            }
        }

    }
}
