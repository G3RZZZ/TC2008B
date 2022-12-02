// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// 
// Gerardo Gutiérrez Paniagua, A01029422
// Mateo Herrera Lavalle A01751912
// Francisco Daniel Salcedo Catalán A01633010
// Regina Rodríguez Sánchez A01284329
// 
// Novimebre 2022
// Octavio Navarro. October 2021
// Camera movement script

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwitchCamera : MonoBehaviour
{
    // Declare variables
    public Transform camera1;
    public Transform camera2;
    public Transform camera3;
    public Transform camera4;
    public float sSpeed = 10.0f;
    public Transform lookTarget;
    private int currentTarget;
    private Transform cameraTarget;



    // Start is called before the first frame update
    void Start()
    {
        // Initialize variables
        currentTarget = 1;
        SetCameraTarget(currentTarget);
    }

    // Update is called once per frame
    void Update()
    {
      // Switch camera when space is pressed
      if (Input.GetKeyDown("space"))
      {
        SwitchCameraNow();
      }
    }

    // Lerp camera orientation and position to empty objects pos
    void FixedUpdate() {
      Vector3 dPos = cameraTarget.position;
      Quaternion drot = cameraTarget.rotation;
      Vector3 sPos = Vector3.Lerp(transform.position, dPos, sSpeed * Time.deltaTime);
      Quaternion srot = Quaternion.Lerp(transform.rotation, drot, sSpeed * Time.deltaTime);
      transform.position = sPos;
      transform.rotation = srot;
      // transform.LookAt(lookTarget.position);
    }

    // Function that sets a ew camera target
    public void SetCameraTarget(int num) {
      switch (num)
      {
        case 1 :
          cameraTarget = camera1.transform;
          break;
        case 2 :
          cameraTarget = camera2.transform;
          break;
        case 3 :
          cameraTarget = camera3.transform;
          break;
        case 4 :
          cameraTarget = camera4.transform;
          break;
      }
    }

    // Function that resets count
    public void SwitchCameraNow(){
      if(currentTarget < 4)
        currentTarget++;
      else  currentTarget = 1;
      SetCameraTarget(currentTarget);
    }

}
