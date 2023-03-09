using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HAndTracking : MonoBehaviour
{
    public UDPConnection udpReceive;
    public GameObject[] handPoint;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        string data = UDPConnection.data;
        
        data = data.Remove(0, 1);
        data = data.Remove(data.Length - 1, 1);

        string[] points = data.Split(',');
        //print(data);
        
        for(int i = 0; i < 21; i++)
        {
            float x1 = (float.Parse(points[i * 3 + 2]) / 100) - 5;
            float y1 = float.Parse(points[i * 3 + 3]) / 100;
            float z1 = float.Parse(points[i * 3 + 4]) / 100;

            float x2 = (float.Parse(points[i * 3 + 65]) / 100) - 5;
            float y2 = float.Parse(points[i * 3 + 66]) / 100;
            float z2 = float.Parse(points[i * 3 + 67]) / 100;

            float distLeft = float.Parse(points[0]) / 10;
            float distRight = float.Parse(points[1]) /10;

            float factor = (distLeft / 20)*3;

            handPoint[i].transform.localPosition = new Vector3(x1, y1, z1+distLeft);
            handPoint[i + 21].transform.localPosition = new Vector3(x2, y2, z2+distRight);
        }

        print(points[0] + " " + points[1]);
    }
}
