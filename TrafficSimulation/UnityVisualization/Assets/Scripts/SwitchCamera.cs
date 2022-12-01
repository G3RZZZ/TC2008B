using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwitchCamera : MonoBehaviour
{
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
        currentTarget = 1;
        SetCameraTarget(currentTarget);
    }

    // Update is called once per frame
    void Update()
    {
      if (Input.GetKeyDown("space"))
      {
        SwitchCameraNow();
      }
    }

    void FixedUpdate() {
      Vector3 dPos = cameraTarget.position;
      Quaternion drot = cameraTarget.rotation;
      Vector3 sPos = Vector3.Lerp(transform.position, dPos, sSpeed * Time.deltaTime);
      Quaternion srot = Quaternion.Lerp(transform.rotation, drot, sSpeed * Time.deltaTime);
      transform.position = sPos;
      transform.rotation = srot;
      // transform.LookAt(lookTarget.position);
    }

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

    public void SwitchCameraNow(){
      if(currentTarget < 4)
        currentTarget++;
      else  currentTarget = 1;
      SetCameraTarget(currentTarget);
    }

}
