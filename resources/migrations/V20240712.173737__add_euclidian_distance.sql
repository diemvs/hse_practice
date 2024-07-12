CREATE OR REPLACE FUNCTION euclidean_distance(arr1 numeric[], arr2 numeric[])
RETURNS numeric AS $$
DECLARE
    dist numeric := 0;
    i int;
BEGIN
    FOR i IN 1 .. array_length(arr1, 1) LOOP
        dist := dist + (arr1[i] - arr2[i]) ^ 2;
    END LOOP;
    RETURN sqrt(dist);
END;
$$ LANGUAGE plpgsql;