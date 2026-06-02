import {getAvailabilities,createAvailability,updateAvailability,deleteAvailability,} from "../services/availabilityService";
import { createContext, useContext, useEffect, useState } from "react";

export const availabilityContext = createContext();

export function AvailabilityProvider({ children }) {
  const [availabilities, setAvailabilities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function listAvailability() {
    setLoading(true);
    try {
      const response = await getAvailabilities();
      setAvailabilities(response.data.results ?? response.data);
    } catch (error) {
      setError('Failed to load availabilities.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function addAvailability(data) {
    try {
      await createAvailability(data);
      await listAvailability();
      return { success: true };
    } catch (error) {
      return { success: false, errors: error.response?.data || {} };
    }
  }

  async function editAvailability(id, data) {
    try {
      const response = await updateAvailability(id, data);
      console.log("SUCCESS:", response);

      await listAvailability();
      return { success: true };
    } catch (error) {
      console.log("ERROR:", error.response?.data);

      return {
        success: false,
        errors: error.response?.data || {},
      };
    }
  }

  async function removeAvailability(id) {
    try {
      await deleteAvailability(id);
      setAvailabilities((prev) => prev.filter((a) => a.id !== id));
      return { success: true };
    } catch (error) {
      return { success: false };
    }
  }

  useEffect(() => {
    listAvailability();
  }, []);

  return (
    <availabilityContext.Provider
      value={{
        availabilities,
        loading,
        error,
        listAvailability,
        addAvailability,
        editAvailability,
        removeAvailability,
      }}
    >
      {children}
    </availabilityContext.Provider>
  );
}

export const useAvailability = () => useContext(availabilityContext);