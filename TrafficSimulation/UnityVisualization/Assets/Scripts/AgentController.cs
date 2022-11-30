// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;
    public bool arrived;

    public AgentData(string id, float x, float y, float z, bool arrived)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.arrived = arrived;
    }
}

[Serializable]
public class TLightData
{
    public string id;
    public bool state;
    public float x, y, z;

    public TLightData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}

[Serializable]

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

[Serializable]

public class TLightsData
{
    public List<TLightData> tLightsState;

    public TLightsData() => this.tLightsState = new List<TLightData>();
}


public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getTLightsEndpoint = "/getTrafficLight";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    TLightsData tlightsdata;
    Dictionary<string, GameObject> agents;
    Dictionary<string, GameObject> tlights;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool carUpdated = false, tLightUpdated = false;
    [SerializeField] GameObject cityGameObject;
    CityMaker city;
    [SerializeField] List<GameObject> prefabList = new List<GameObject>();
    public GameObject agentPrefab;
    public int NAgents, width, height;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        tlightsdata = new TLightsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        tlights = new Dictionary<string, GameObject>();

        city = cityGameObject.GetComponent(typeof(CityMaker)) as CityMaker;

        // floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        // floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            carUpdated = false;
            tLightUpdated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (carUpdated && tLightUpdated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetTrafficLightData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetTrafficLightData());
        }
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach(AgentData agent in agentsData.positions)
            {
                if (agent.arrived && prevPositions.ContainsKey(agent.id))
                {
                  prevPositions.Remove(agent.id);
                  currPositions.Remove(agent.id);
                  Destroy(agents[agent.id]);
                  agents.Remove(agent.id);
                } else
                {  
                  Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                      if(!prevPositions.ContainsKey(agent.id))
                      {
                          prevPositions[agent.id] = newAgentPosition;
                          int prefabIndex = UnityEngine.Random.Range(0,prefabList.Count);
                          GameObject chosenPrefab = prefabList[prefabIndex];
                          agents[agent.id] = Instantiate(chosenPrefab, newAgentPosition, Quaternion.identity);
                      }
                      else
                      {
                          Vector3 currentPosition = new Vector3();
                          if(currPositions.TryGetValue(agent.id, out currentPosition))
                              prevPositions[agent.id] = currentPosition;
                          currPositions[agent.id] = newAgentPosition;
                      }
                }
            }

            carUpdated = true;
        }
    }

    IEnumerator GetTrafficLightData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTLightsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            tlightsdata = JsonUtility.FromJson<TLightsData>(www.downloadHandler.text);

            foreach(TLightData tlight in tlightsdata.tLightsState)
            {
                Vector3 lightPos = new Vector3(tlight.x, tlight.y, tlight.z);
                GameObject light = city.tile_lights[lightPos];
                Light actual_light = light.GetComponentInChildren(typeof(Light)) as Light;
                if (tlight.state)
                {
                  actual_light.color = Color.green;
                  
                } else
                {
                  actual_light.color = Color.red;
                }
            }
          tLightUpdated = true;
        }

      }
}
